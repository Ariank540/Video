import {AbsoluteFill, Composition, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Audio} from '@remotion/media';
const Composite = () => {
 const frame=useCurrentFrame();
 const {fps}=useVideoConfig();
 const subject=staticFile(`subject/${String(Math.min(frame,59)).padStart(5,'0')}.png`);
 const full={position:'absolute' as const,width:'100%',height:'100%'};
 return <AbsoluteFill style={{backgroundColor:'#101112'}}>
  <Img src={staticFile('cabin.png')} style={{...full,filter:'brightness(1.12) saturate(0.92)'}} />
  <Img src={subject} style={{...full,filter:'drop-shadow(2px 3px 4px rgba(0,0,0,0.23))'}} />
  <Img src={staticFile('cabin.png')} style={{...full,filter:'brightness(1.12) saturate(0.92)',clipPath:'polygon(0 82.7%, 100% 86.9%, 100% 100%, 0 100%)'}} />
  <Img src={subject} style={{...full,clipPath:'polygon(0 74%, 22% 74%, 22% 100%, 0 100%)'}} />
  <Audio src={staticFile('audio.wav')} premountFor={fps}/>
 </AbsoluteFill>;
};
export const Root=()=> <Composition id="UrusCompositeTest" component={Composite} width={540} height={960} fps={30} durationInFrames={60}/>;
