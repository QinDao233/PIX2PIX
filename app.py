from flask import Flask, request, render_template_string, send_file
import os
import subprocess
import tempfile

app = Flask(__name__)

# 定义 HTML 模板
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CycleGAN and pix2pix Web Interface</title>
</head>
<body>
    <h1>CycleGAN and pix2pix Web Interface</h1>
    <form method="post" enctype="multipart/form-data">
        <label for="model_type">选择模型类型:</label>
        <select name="model_type" id="model_type">
            <option value="cycle_gan">CycleGAN</option>
            <option value="pix2pix">pix2pix</option>
        </select><br><br>
        <label for="image">上传图片:</label>
        <input type="file" name="image" id="image"><br><br>
        <input type="submit" value="转换">
    </form>
    {% if result_image %}
        <h2>转换结果</h2>
        <img src="{{ result_image }}" alt="转换结果">
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        model_type = request.form.get('model_type')
        image = request.files['image']

        # 保存上传的图片到临时文件
        temp_dir = tempfile.mkdtemp()
        image_path = os.path.join(temp_dir, image.filename)
        image.save(image_path)

        if model_type == 'cycle_gan':
            # 假设你已经下载了预训练的 horse2zebra 模型
            command = [
                'python', 'test.py',
                '--dataroot', temp_dir,
                '--name', 'horse2zebra_pretrained',
                '--model', 'test',
                '--no_dropout'
            ]
        elif model_type == 'pix2pix':
            # 假设你已经下载了预训练的 facades_label2photo 模型
            command = [
                'python', 'test.py',
                '--dataroot', temp_dir,
                '--direction', 'BtoA',
                '--model', 'pix2pix',
                '--name', 'facades_label2photo_pretrained'
            ]

        try:
            # 执行命令
            subprocess.run(command, check=True)

            # 假设结果图片保存的路径
            result_image_path = os.path.join('results', f'{model_type}_pretrained', 'latest_test', 'images', image.filename)

            return render_template_string(html_template, result_image=result_image_path)
        except subprocess.CalledProcessError as e:
            return f"执行命令时出错: {e}"

    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
