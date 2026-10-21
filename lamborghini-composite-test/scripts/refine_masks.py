from pathlib import Path
import cv2,numpy as np,json
root=Path(__file__).resolve().parents[1]
prior=root.parent/'lamborghini-transformation/research/output'
stats=[]
for j in range(60):
 rgb=cv2.imread(str(prior/'source-frames'/f'{j:05}.png'))
 a=cv2.imread(str(prior/f'alpha-{j+75:04}.png'),0)
 old=a.copy()
 hsv=cv2.cvtColor(rgb,cv2.COLOR_BGR2HSV)
 # Remove neutral office chair outside the navy shirt on frame-right.
 yy,xx=np.mgrid[:960,:540]
 chair=(xx>505)&(yy>620)&(hsv[:,:,1]<72)&(hsv[:,:,2]<175)
 # Keep skin/watch and remove only outside the blue-clothing silhouette.
 blue=((hsv[:,:,0]>95)&(hsv[:,:,0]<130)&(hsv[:,:,1]>70)&(hsv[:,:,2]<180)).astype(np.uint8)
 blue=cv2.dilate(blue,np.ones((3,3),np.uint8))
 chair=chair&(blue==0)
 a[chair]=0
 # Can localization from its cyan label, restricted to the upper-body ROI.
 label=((hsv[:,:,0]>=80)&(hsv[:,:,0]<=110)&(hsv[:,:,1]>85)&(hsv[:,:,2]>100)&(xx>170)&(xx<380)&(yy>350)&(yy<660)).astype(np.uint8)
 n,labels,cs,cent=cv2.connectedComponentsWithStats(label)
 cup_pixels=0
 if n>1:
  k=1+np.argmax(cs[1:,cv2.CC_STAT_AREA])
  if cs[k,cv2.CC_STAT_AREA]>120:
   x,y,w,h,_=cs[k]
   # Fill enclosed alpha holes locally, not all finger gaps or face silhouette.
   binary=(a>100).astype(np.uint8)*255
   contours,_=cv2.findContours(binary,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
   filled=np.zeros_like(a);cv2.drawContours(filled,contours,-1,255,cv2.FILLED)
   roi=(xx>=max(0,x-20))&(xx<min(540,x+w+5))&(yy>=max(0,y-50))&(yy<min(960,y+h+25))
   repair=roi&(filled>0)
   cup_pixels=int(((a<250)&repair).sum()); a[repair]=255
 # Fully opaque original subject interiors; preserve soft hair perimeter.
 a[a>245]=255
 # Do not use RVM's predicted RGB, warping, face smoothing or subject color filters.
 # Edge-only white-wall decontamination; face/skin and opaque RGB remain untouched.
 edge=(a>12)&(a<250)&(yy<475)&(yy>330)&(xx>135)&(xx<350)
 skin=(hsv[:,:,0]<30)&(hsv[:,:,1]>40)
 edge &= ~skin
 edge &= ~((xx>130)&(xx<350)&(yy>400)&(yy<650))
 af=np.maximum(a.astype(np.float32)/255,.12)
 wall=np.median(rgb[250:330,50:120].reshape(-1,3),axis=0)
 clean=np.clip((rgb.astype(np.float32)-(1-af[:,:,None])*wall)/af[:,:,None],0,255).astype(np.uint8)
 result=rgb.copy(); result[edge]=clean[edge]
 bgra=np.dstack([result,a])
 cv2.imwrite(str(root/'public/subject'/f'{j:05}.png'),bgra)
 assert np.array_equal(bgra[:,:,:3][~edge],rgb[~edge])
 stats.append({'frame':j,'can_hole_pixels_filled':cup_pixels,'chair_pixels_removed':int(((old>0)&chair).sum())})
(root/'mask-refinement.json').write_text(json.dumps({'opaque_and_face_rgb_preserved':True,'hair_boundary_only_decontaminated':True,'frames':stats},indent=2))
print('60 PNGs saved; protected RGB unchanged; hair-boundary decontamination only; repairs',sum(x['can_hole_pixels_filled'] for x in stats),'chair removals',sum(x['chair_pixels_removed'] for x in stats))
