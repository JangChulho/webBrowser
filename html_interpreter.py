import ply.lex as lex
import ply.yacc as yacc
import graphics
import html_tokens
import html_grammar
import javascript_tokens
import javascript_grammar
import javascript_interpreter

htmllexer = lex.lex(module=html_tokens)
htmlparser = yacc.yacc(module=html_grammar, tabmodule="parsetabhtml")
jslexer = lex.lex(module=javascript_tokens)
jsparser = yacc.yacc(module=javascript_grammar, tabmodule="parsetabjs")
    
def interpret(ast):
    for node in ast:
        nodetype = node[0]
        if nodetype == "word-element":            
            graphics.word(node[1])
        elif nodetype == "tag-element":           
            tagname = node[1]
            tagargs = node[2]
            subast = node[3]
            closetagname = node[4]
            if (tagname != closetagname):
                graphics.warning("(mistmatched " + tagname + " " + closetagname + ")")                
            else:
                graphics.begintag(tagname, tagargs)                
                interpret(subast)
                graphics.endtag()
        elif nodetype == "javascript-element":            
            jstext = node[1]
            jsast = jsparser.parse(jstext, lexer=jslexer)
            result = javascript_interpreter.interpret(jsast)
            htmlast = htmlparser.parse(result, lexer=htmllexer)
            interpret(htmlast)        
    
webpage = """<html>
<img src="test.jpg"></img>
<h1>Codin9Cafe</h1>
<img src="test2.jpg"></img>
<h2>Level One Headings Use (H2) Tags</h2> 
<p>Paragraphs use (P) tags. Unordered lists use (UL) tags.
<ul>
  <li> List items use (LI) tags. </li> 

  <!-- You should update this HTML until the order and nesting of
       the tags match the reference image. -->
  <li> Text can be <b>bold (B)</b>, <i>italic (I)</i>, <small>small 
  (SMALL)</small>, <big>big (BIG)</big>, or look like a <tt>typewriter
  (TT)</tt>. </li>
  <li> There are also ordered lists that use (OL) tags. Let's make one
  nested inside our current list item.
    <ol>
    <li> Text can also be <strong>strong (STRONG)</strong> or <em>emphasized (EM)</em>, which typically renders like bold and italics.</li>
    <li> Webpages can have <a href="http://www.google.com">hyperlinks</a>. </li>
    </ol>
  </li>  
</ul>
</p>
<h2>MOOC(Massive Open Online Course) List</h2>
<ul>
<li>Udacity : <a href="https://www.udacity.com">https://www.udacity.com</a></li>
<li>Cousera : <a href="https://www.coursera.org">https://www.coursera.org</a></li>
<li>edX : <a href="https://www.edx.org">https://www.edx.org</a></li>
</ul>
<h2>Meet</h2>
<ul>
<li>Place : BookAndBeans</li>
<li>Time : 3/18(Wed) 7PM</li>
<li>Tel : 010-3440-8535</li>
<li>facebook group: <a href="https://www.facebook.com/groups/codin9cafe">https://www.facebook.com/groups/codin9cafe</a></li>
</ul><br />
<script type="text/javascript">
function tricky(i) {
  write("<h2>javascript test : ");
  while(i>=0){   
  if ((i % 2) == 1) {
    write("<big>");
    write(i); 
    write("</big>"); 
  } else {
    write("<i>");
    write(i); 
    write("</i>"); 
  } ;  
  i = i - 1;
  } ;
  write("</h2>");
}
tricky(10);
</script>
</html>"""

htmlast = htmlparser.parse(webpage, lexer=htmllexer)
graphics.initialize()
interpret(htmlast)
graphics.finalize()
