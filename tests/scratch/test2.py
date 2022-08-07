from src.terraform_vaccum.renderers import TFileRenderer
from src.terraform_vaccum.template_processor import Template

tmp = Template('data2/test.t.yml', 'data/simple.json')
renderer: TFileRenderer = tmp.run()
renderer.adjust_indent()
print(renderer.render())
renderer.save()
