---
title: Jeecg-Boot-前端积累.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开源项目
categories: 开源项目
---
---
title: Jeecg-Boot-前端积累.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开源项目
categories: 开源项目
---
0、接口地址切换
vue.config.js
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7cd6866211405f95.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1、获取复选框选中项
>   console.log(this)
        console.log(this.selectionRows)
        console.log(this.selectedRowKeys)

2、JPopup 组件没有开源，会提示找不到

import JPopup from '@/components/jeecgbiz/jpopup'


3、发起请求实例
~~~
    // debugger
        console.log(rows,idstr)
        console.log(this.selectedRowKeys)
        let join = this.selectedRowKeys.join(",")

        var that = this
        httpAction('/ipaid/boxOutOfStock', { 'ids': join, "departId": idstr }, 'post').then((res) => {
          if (res.success) {
            that.$message.success(res.message)
            that.$emit('ok')
          } else {
            that.$message.warning(res.message)
          }
        }).finally(() => {
          that.confirmLoading = false
           this.loadData();
        })
~~~

4、刷新页面
  this.loadData();


5、部门弹出窗组件

触发按钮
~~~
      <a-button  @click="openModal" type="primary" icon="import" v-has="'box:ck'">管理员出库到单位 </a-button>
~~~

部门选择弹出窗组件
~~~
    <j-select-depart-modal
      ref="innerDepartSelectModal"
      :modal-width="modalWidth"
      :multi="multi"
      :rootOpened="rootOpened"
      :depart-id="departIds"
      @ok="handleOK"
      @initComp="initComp"/>

~~~

数据构造
~~~
<script>

  import JSelectDepartModal from '../../components/jeecgbiz/modal/JSelectDepartModal'

  export default {
    name: 'TbBoxList',
    mixins: [JeecgListMixin],
    components: {
      JSelectDepartModal
    },
    props:{
      modalWidth:{
        type:Number,
        default:500,
        required:false
      },
      multi:{
        type:Boolean,
        default:false,
        required:false
      },
      rootOpened:{
        type:Boolean,
        default:true,
        required:false
      },
    },
    data() {
      return {
        form: this.$form.createForm(this),
        description: '箱子管理页面',
     }
   
    },
    computed: {
  
    },

    created() {
      this.departIds = this.value
    },
    methods: {

      initComp(departNames){
        console.log(departNames)
        this.departNames = departNames
      },
     ,
     openModal(){
        this.$refs.innerDepartSelectModal.show()
      },
      handleOK(rows, idstr) {
        let join = this.selectedRowKeys.join(",")
        var that = this
        httpAction('/ipaid/boxOutOfStock', { 'ids': join, "departId": idstr }, 'post').then((res) => {
          if (res.success) {
            that.$message.success(res.message)
            that.$emit('ok')
          } else {
            that.$message.warning(res.message)
          }
        }).finally(() => {
          that.confirmLoading = false
          this.loadData();
        })

      }
    
      
  }
</script>
~~~
