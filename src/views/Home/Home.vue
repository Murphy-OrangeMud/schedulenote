
<template>
  <div id="home">
    <br>
    <h1>开始写markdown吧！</h1>
    <div class="note" style="position:relative;margin-left:10%;margin-right:10%">
      <v-md-editor v-model="text" id = "printMe" height="800px" @save="Save">
      </v-md-editor><br>
    </div>

  </div>
</template>

<script>
/* eslint-disable */
function Template(tpl) {
  var
      fn,
      match,
      code = ['var r=[];\nvar _html = function (str) { return str; };'],
      re = /\{\s*([a-zA-Z\.\_0-9()]+)(\s*\|\s*safe)?\s*\}/m,
      addLine = function (text) {
          code.push('r.push(\'' + text.replace(/\'/g, '\\\'').replace(/\n/g, '\\n').replace(/\r/g, '\\r') + '\');');
      };
  while (match = re.exec(tpl)) {
      if (match.index > 0) {
          addLine(tpl.slice(0, match.index));
      }
      if (match[2]) {
          code.push('r.push(String(this.' + match[1] + '));');
      }
      else {
          code.push('r.push(_html(String(this.' + match[1] + ')));');
      }
      tpl = tpl.substring(match.index + match[0].length);
  }
  addLine(tpl);
  code.push('return r.join(\'\');');
  fn = new Function(code.join('\n'));
  this.render = function (model) {
      return fn.apply(model);
  };
}
function downloadFile(fileName, content){
  var aLink = document.createElement('a');
  var blob = new Blob([content]);
  var evt = document.createEvent("HTMLEvents");
  aLink.download = fileName;
  aLink.href = URL.createObjectURL(blob);
  aLink.click();
}

let tplhtml = ' <html>\
<head>\
<meta charset="utf-8">\
<meta name="viewport" content="width=device-width, initial-scale=1, minimal-ui">\
<title>GitHub Markdown CSS demo</title>\
<link rel="stylesheet" href="https://sindresorhus.com/github-markdown-css/github-markdown.css">\
<style>\
	@media (min-width: 768px) {\
		.markdown-body {\
			box-sizing: border-box;\
			min-width: 200px;\
			max-width: 980px;\
			margin: 0 auto;\
			padding: 45px;\
		}\
	}\
</style>\
</head>\
<body>\
<article class="markdown-body">\
{content}\
</article>\
</body>\
</html>'

let styleCode = '	#edit {display: flex; justify-content: space-between;}\
    #content {width: 49%;float: left;height: auto;}\
    .button {\
        color: #fff;\
        background-color: #009a61;\
        border-color: #008151;\
        padding: 0 13px;\
        font-size: 14px;\
        border-radius: 4px;\
        margin: 10px;\
    }\
    #show{width: 50%; border:  1px solid  #ddd; padding: 50px; box-sizing: border-box;float: left;height: auto;}\
	\
	.hljs-comment,.hljs-quote {\
	 color:#989498\
	}\
	.hljs-variable,.hljs-template-variable,.hljs-attribute,.hljs-tag,.hljs-name,.hljs-selector-id,.hljs-selector-class,.hljs-regexp,.hljs-link,.hljs-deletion {\
	 color:#dd464c\
	}\
	.hljs-number,.hljs-built_in,.hljs-builtin-name,.hljs-literal,.hljs-type,.hljs-params {\
	 color:#fd8b19\
	}\
	.hljs-class .hljs-title {\
	 color:#fdcc59\
	}\
	.hljs-string,.hljs-symbol,.hljs-bullet,.hljs-addition {\
	 color:#8fc13e\
	}\
	.hljs-meta {\
	 color:#149b93\
	}\
	.hljs-function,.hljs-section,.hljs-title {\
	 color:#1290bf\
	}\
	.hljs-keyword,.hljs-selector-tag {\
	 color:#c85e7c\
	}\
	.hljs {\
	 display:block;\
	 background:#322931;\
	 color:#b9b5b8;\
	 padding:0.5em\
	}\
	.hljs-emphasis {\
	 font-style:italic\
	}\
	.hljs-strong {\
	 font-weight:bold\
  }'
  
import jsPDF from 'jspdf'

export default {
  data () {
    return {
      text: 'Hello'
    }
  },
  methods: {
    Save (text, htmlCode) {
      var tpl = new Template(tplhtml);
      var s = tpl.render({
          title: "markdown",
          style:styleCode,
          content:htmlCode
      });
      downloadFile("markdown.html",s);
      /*
      System.out.println(pdfPath);
      StyleSheet st = new StyleSheet();
      st.loadTagStyle("body", "leading", "16,0");
      // step 1
      Document document = new Document(PageSize.A4);
      // step 2
      PdfWriter.getInstance(document, new FileOutputStream(pdfPath));
      // step 3
      document.open();
      // step 4
      BaseFont bfChinese = BaseFont.createFont("STSong-Light", "UniGB-UCS2-H", BaseFont.NOT_EMBEDDED);
      Font FontChinese = new Font(bfChinese, 12, Font.NORMAL);
      List<Element> p = HTMLWorker.parseToList(dome_2(html), st);
      System.out.println("who is 0:"+p.get(0).getChunks().get(0));
      for (Element aP : p) {
          for (int m = 0; m < aP.getChunks().size(); m++) {
              Paragraph pCode = new Paragraph(aP.getChunks().get(m).toString(), FontChinese);
              document.add(pCode);
          }
      }
      // step 5
      document.close();
      /*var doc = new jsPDF('p', 'pt', 'a4')
      var elementHTML = html
      var specialElementHandlers = {
        '#elementH': function (element, renderer) {
          return true
        }
      }

      doc.html(DATA.innerHTML, {
        'x': 15,
        'y': 15,
        'width': 170,
        'elementHandlers': specialElementHandlers
      });

      doc.save('sample.pdf')*/
    }
  }
}
</script>
