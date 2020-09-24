<template>
  <div class="ResultFrame">
    <h3>Result</h3>
    <div>
      <SingleLCAResult v-for="(singleLCAResult, index) in displayableResult.singleLCA"  :key="index" :singleLCAResult="singleLCAResult"></SingleLCAResult>
    </div>
    
  </div>
</template>

<script>
import VueVirtualTable from 'vue-virtual-table'
import SingleLCAResult from './SingleLCAResult.vue'
export default {
  name: 'ResultFrame',
  components: {
    VueVirtualTable,
    SingleLCAResult
  },
  props: {
    moduleList: Array,
    displayableResult: {
      type: Array,
      required: true
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
