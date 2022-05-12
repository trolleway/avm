
# Generate titles from all txt files in directory

ffmpeg -y -f lavfi -i color=size=3840x2160:duration=3:rate=60:color=black \
-filter_complex "[0:v]drawtext=fontfile=Jura.ttf:textfile=text.txt:fontsize=260:fontcolor=adadad:alpha='if(lt(t,0),0,if(lt(t,0.5),(t-0)/0.5,if(lt(t,2.5),1,if(lt(t,3),(0.5-(t-2.5))/0.5,0))))':x=(w-text_w)/2:y=(h-text_h)/2" \
-c:v libx265 -crf 26 -preset fast \
output.mp4 && ffplay output.mp4

#http://ffmpeg.shanewhite.co/
