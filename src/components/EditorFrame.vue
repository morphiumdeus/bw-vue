<template>
  <div class="EditorFrame">
    <h3>Editor</h3>
    <div class="headerButtons">
      <sui-button v-on:click="saveEditorText">Save (Ctrl-S)</sui-button>
      <sui-button v-on:click="run">Run (Ctrl-R)</sui-button>
    </div>
    
    <div id="monaco-editor-container" v-on:keydown.ctrl.s.stop.prevent="saveEditorText">
    </div>
  </div>
</template>

<script>
import * as monaco from 'monaco-editor'
import MonacoEditor from 'vue-monaco'
//import * as jsyaml from 'js-yaml'

export default {
  name: 'EditorFrame',
  props: {
    moduleList: Array
  },
  
  mounted: function(){
    var vm = this
    monaco.languages.register({id: 'yaml'})
    monaco.languages.registerCompletionItemProvider('yaml', {
      provideCompletionItems: function(model, position) {
        let textUntilPosition = model.getValueInRange({startLineNumber: 1, startColumn: 1, endLineNumber: position.lineNumber, endColumn: position.column})
        let textUntilPositionByLine = textUntilPosition.split("\n")
        let curIndent = 0, smallestIndent = 999999,
          hierarchy = []
        let lastLineByWord = textUntilPositionByLine[position.lineNumber-1].replace(/\W+/g,' ').split(' ');
        for(let i=lastLineByWord.length -1;i>0;i--){
          console.log(lastLineByWord[i])
          if(lastLineByWord[i] != '') hierarchy.push(lastLineByWord[i])
        }
        for(var lineNumber=position.lineNumber-2;lineNumber>0;lineNumber--){
          curIndent = numberOfTabs(textUntilPositionByLine[lineNumber])
          if( curIndent < smallestIndent){
            hierarchy.push(textUntilPositionByLine[lineNumber].replace(/^\s*/gm, '').split(/[,:]+/)[0])
          }
          smallestIndent = Math.min(curIndent,smallestIndent)
        }
        console.log(hierarchy)
        return vm.createProposals(hierarchy)
                  .then(rep => {
                    let counter = 0
                    return rep.map(x => {
                      x.sortText = String.fromCharCode(97 + counter++)
                      x.kind = (/^monaco.languages.CompletionItemKind./.test(x.kind) ? eval(x.kind.replace("(", "")) : 0)
                      x.insertText = {value: x.insertText}
                      return x})
                  })
        
        // return {suggestions: rep}; this worked with a different version?
        
      }
    })
    vm.setEditor(monaco.editor.create(document.getElementById('monaco-editor-container'), {
      value: vm.loadEditorText(),
      language: 'yaml',
    }))
  },
  methods: {
    setEditor: function(editor){this.editor = editor},
    getEditor: function(){return this.editor},
    saveEditorText: function(){
      if (typeof(localStorage) !== "undefined") {
        localStorage.setItem('editorValue', this.getEditor().getValue());
      }
    },
    run: function(){
      console.log(location.protocol+'//'+location.hostname+":5555/run");
      this.axios.post(location.protocol+'//'+location.hostname+":5555/run", this.getEditor().getValue(), {
        headers: {
            'Content-Type': 'application/x-yaml',
        }
      }).then(response => {
        console.log('axios log: ', response);
        this.$emit('broadcastResults', response.data);
      })

    },
    loadEditorText: function(){
      var editorValue = `
---
# To be able to split the document, we create a master "project" key that will be used to run the brightway2 project stuff
project: 
  databases:
    ecoInvent3: &ei3
      type: SingleOutputEcospold2Importer
      name: ecoinvent 3.1 cutoff
      location: /Users/cmutel/Documents/LCA Documents/Ecoinvent/3.1/cutoff/datasets
    forwast: &forwast
      type: SingleOutputEcospold1Importer
      name: forwast
      location: /Users/cmutel/Downloads/FORWAST-ecospold1
  activities:`
      if (typeof(localStorage) !== "undefined") {
        if(localStorage.getItem('editorValue')){
          editorValue = localStorage.getItem('editorValue')
        }
      } else {
        // Sorry! No Web Storage support..
      }
      return editorValue
    },
    createProposals: function(hierarchy) {
      return this.axios.post(location.protocol+'//'+location.hostname+":5555/getAutocomplete", hierarchy).then(response => {
            return response.data
      })
    }
  }
}

function numberOfTabs(text) {
  var count = 0, index = 0
  while (text.charAt(index++) === "\t" || text.charAt(index++) === " ") {
    count++
  }
  return count
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.EditorFrame {
  height: 100%;
}
#monaco-editor-container {
    width: 100%;
    min-height: 600px;
    position: relative;
    top: 0px;
    bottom: 0px;
}
.editor {
  width: 600px;
  height: 800px;
}
</style>
