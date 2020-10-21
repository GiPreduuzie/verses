git clean -fX

if [ -z $TAG ];
then
TAG="$(date +"%Y.%m.%d.%H.%M.%S")";
OUTPUT="verses";
fi

python3 txt_to_tex.py

sed -i "s/VERSION/v$TAG/" cover.tex
pdflatex -synctex=1 -interaction=nonstopmode -output-directory=. -jobname="$OUTPUT" main.tex
# run build twice because of latex compilation process
# after first run TOC is empty
pdflatex -synctex=1 -interaction=nonstopmode -output-directory=. -jobname="$OUTPUT" main.tex
sed -i "s/v$TAG/VERSION/" cover.tex

# git clean -fX