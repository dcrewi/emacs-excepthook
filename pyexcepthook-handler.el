; Copyright (c) 2012 David Creswick
;
; Permission is hereby granted, free of charge, to any person obtaining
; a copy of this software and associated documentation files (the
; "Software"), to deal in the Software without restriction, including
; without limitation the rights to use, copy, modify, merge, publish,
; distribute, sublicense, and/or sell copies of the Software, and to
; permit persons to whom the Software is furnished to do so, subject to
; the following conditions:
;
; The above copyright notice and this permission notice shall be
; included in all copies or substantial portions of the Software.
;
; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
; EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
; MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
; NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
; LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
; OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
; WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

(defun pyexcepthook-handler (type value stack-frames)
  (let ((buffer (get-buffer-create "*python-exception*"))
	(exc-msg (concat type (if (zerop (length value))
			        ""
				(concat ": " value)))))
    (set-buffer buffer)
    (setq buffer-read-only nil)
    (erase-buffer)
    (insert "Traceback (most recent call last):\n")
    (dolist (frame stack-frames)
      (let* ((filename (pop frame))
	     (line-no  (pop frame))
	     (fnc-name (pop frame))
	     (line-text(pop frame))
	     (text     (format "  File code %S, line %d, in %s\n    %s\n"
			       filename line-no fnc-name line-text)))
	(if (and (<= 3 (length filename))
		 (string= ".py" (substring filename -3)))
	  (insert-button text
	     'help-echo "mouse-2, RET: visit source line"
	     'face nil
	     'follow-link t
	     'filename filename
	     'line-no line-no
	     'exc-msg exc-msg
	     'action
	     (lambda (btn)
	       (find-file (button-get btn 'filename))
	       (goto-char 0)
	       (forward-line (- (button-get btn 'line-no) 1))
	       (message (button-get btn 'exc-msg))))
	  (insert text))))
    (insert exc-msg)
    (insert "\n")
    (set-buffer-modified-p nil)
    (setq buffer-read-only t)
    (switch-to-buffer buffer)
    nil))
