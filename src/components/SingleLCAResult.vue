<template>
  <div class="SingleLCAResult">
      <div>{{functionalUnit}}</div>
      <vue-virtual-table :min-width="200" :config="tableConfig" :data="singleLCAResult.results"
        :selectable="tableAttribute.selectable"
        :enableExport="tableAttribute.enableExport"
        :hoverHighlight="tableAttribute.hoverHighlight"
        :language="tableAttribute.language">
      </vue-virtual-table>    
  </div>
</template>

<script>
import VueVirtualTable from 'vue-virtual-table'
export default {
  name: 'SingleLCAResult',
  components: {
    VueVirtualTable
  },
  props: {
    moduleList: Array,
    singleLCAResult: {
      type: Object,
      required: true
    }
  },
  data: function () {
    return {
      isOpen: false,
      tableConfig: [
        {prop: 'name', name: 'Category', searchable: false, sortable: true},
        {prop: 'amount', sortable: true},
        {prop: 'unit'}
      ],
      tableAttribute: {
        selectable: true,
        enableExport: false,
        hoverHighlight: true,
        language: "en"
      }
    }
  },
  computed: {
    functionalUnit(){
        console.log(this.singleLCAResult)
        return "Functional unit: " + this.singleLCAResult['inputs']['amount'] +" "+ this.singleLCAResult['inputs']['unit']+ " "+  this.singleLCAResult['inputs']['name'];
    }
  },
  methods: {
    writeScientificNum(p_num, p_precision) {
      var n = Math.round(Math.log10(p_num));
      var m = (p_num * (Math.pow(10,Math.abs(n)))).toFixed(p_precision);
      return m.toString() + ' x 10 E' + n.toString();
}
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
