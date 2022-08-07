from src.terraform_vaccum.renderers import TFileRenderer
from src.terraform_vaccum.template_processor import TemplateProcessor

tmp = TemplateProcessor('data2/test.t.yml', 'data/test.json')
renderer: TFileRenderer = tmp.run()
renderer.adjust_indent()
print(renderer.render())
renderer.save()
