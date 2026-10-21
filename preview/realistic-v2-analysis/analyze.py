from pathlib import Path
import cv2,numpy as np,csv,json,hashlib
P=Path(__file__).resolve().parent;repo=P.parents[1]
source=repo/'ee413ec1859649279ecf96c18a9981ca.mov';test=repo/'preview/lamborghini-composite-test-v1.mp4'
def read(path):
 cap=cv2.VideoCapture(str(path)); frames=[]
 while True:
  ok,f=cap.read()
  if not ok:break
  frames.append(f)
 cap.release();return frames
original=read(source); composite=read(test)
rows=[];prev=None
for i,f in enumerate(original):
 gray=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
 d=float(np.abs(gray[:300].astype(float)-prev[:300]).mean()) if prev is not None else 0.
 rows.append({'frame':i,'nominal_seconds':i/30,'top_background_mean_abs_change':d,'frame_laplacian_variance':float(cv2.Laplacian(gray,cv2.CV_64F).var())});prev=gray.astype(float)
with (P/'original-frame-checks.csv').open('w') as fp:
 w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
rows=[]
for i,f in enumerate(composite):
 a=cv2.imread(str(repo/'lamborghini-composite-test/public/subject'/f'{i:05}.png'),-1)[:,:,3]
 rows.append({'frame':i,'source_frame':i+75,'original_seconds':2.5+i/30,'soft_alpha_pixels':int(((a>12)&(a<243)).sum()),'opaque_pixels':int((a==255).sum())})
with (P/'composite-frame-checks.csv').open('w') as fp:
 w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for page in range(4):
 canvas=np.zeros((3*264,5*270,3),np.uint8)
 for k in range(15):
  i=page*15+k;y=(k//5)*264;x=(k%5)*270
  pair=np.concatenate([cv2.resize(original[i+75],(135,240)),cv2.resize(composite[i],(135,240))],axis=1)
  canvas[y:y+240,x:x+270]=pair
  cv2.putText(canvas,f'v1 {i:02} / src {i+75:03}',(x+3,y+257),cv2.FONT_HERSHEY_SIMPLEX,.4,(255,255,255),1)
 cv2.imwrite(str(P/f'comparison-{page+1}.jpg'),canvas)
summary={'source_frames_decoded':len(original),'v1_frames_decoded':len(composite),'paired_frames_analyzed':min(60,len(composite)),'new_video_created':False,'reason':'No available validated replacement pipeline; do not repeat static-plate approach','original_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'v1_sha256':hashlib.sha256(test.read_bytes()).hexdigest(),'warning':'CSV diagnostics are not calibrated realism scores; visual paired frames are provided for inspection.'}
(P/'checks.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
