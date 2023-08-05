(TeX-add-style-hook
 "pattern"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "12pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("geometry" "paper=a4paper" "margin=5mm" "headsep=0cm" "footskip=0cm" "dvips" "") ("inputenc" "utf8")))
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art12"
    "geometry"
    "inputenc"
    "tikz"
    "calc"))
 :latex)

