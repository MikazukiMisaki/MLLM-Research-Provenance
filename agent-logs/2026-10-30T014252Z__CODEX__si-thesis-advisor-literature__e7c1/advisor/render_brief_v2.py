from pathlib import Path
import textwrap,re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parent
lines=(root/'ADVISOR_BRIEF_V2.md').read_text().splitlines()
fig=plt.figure(figsize=(8.27,11.69),facecolor='white')
y=11.13
for line in lines:
 if not line.strip():
  y-=0.045
  continue
 if line.startswith('|---'): continue
 if line.startswith('# '):
  fig.text(.53/8.27,y/11.69,line[2:],fontsize=15,weight='bold',color='#10273f',va='top');y-=.31;continue
 if line.startswith('|'):
  cells=[x.strip() for x in line.strip('|').split('|')]
  if len(cells)==2:
   header=cells[0]=='Policy'
   fig.text(.73/8.27,y/11.69,cells[0],fontsize=10.0,weight='bold' if header else 'normal',va='top')
   fig.text(5.1/8.27,y/11.69,cells[1],fontsize=10.0,weight='bold' if header else 'normal',va='top')
   y-=.19
  continue
 line=re.sub(r'\*\*([^*]+)\*\*',r'\1',line).strip('*')
 for segment in textwrap.wrap(line,width=94,break_long_words=False,break_on_hyphens=False):
  fig.text(.53/8.27,y/11.69,segment,fontsize=10.0,color='#1a2734',va='top')
  y-=.178
 y-=.045
if y<.42:
 raise SystemExit(f'Content would exceed one page: remaining y={y:.3f} in')
fig.text(.53/8.27,.31/11.69,'Working draft • 30 October 2026 • For discussion',fontsize=7,color='#64748b',va='bottom')
fig.canvas.draw()
renderer=fig.canvas.get_renderer()
for t in fig.texts:
 box=t.get_window_extent(renderer)
 if box.x0<0 or box.y0<0 or box.x1>fig.bbox.width or box.y1>fig.bbox.height:
  raise SystemExit('Text exceeds page: '+t.get_text()[:50])
fig.savefig(root/'SI_U1_RESEARCH_UPDATE_FOR_ADVISOR_V2.pdf',format='pdf')
fig.savefig(root/'SI_U1_RESEARCH_UPDATE_FOR_ADVISOR_V2_preview.png',dpi=140)
print(f'One page; content bottom y={y:.3f} inches')
