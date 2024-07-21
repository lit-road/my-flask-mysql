<script setup lang="ts">
// const store = useStore()
import axios from 'axios'
import { ref, reactive } from 'vue'
import type { FormRules } from 'element-plus'
import { de } from 'element-plus/es/locales.mjs';

interface RuleForm {
  id?: number
  name: string
  gender: 'male' | 'female'
}

const dialogFormVisible = ref(false)
const tableData = ref([
  { id: '1', name: '王小虎', gender: 'male' },
  { id: '1', name: '王小虎', gender: 'male' },
  { id: '1', name: '王小虎', gender: 'male' },
])
const form = reactive<RuleForm>({
  name: '',
  gender: 'male',
})
const rules = reactive<FormRules<RuleForm>>({
  name: [
    { required: true, message: 'Please input name', trigger: 'blur' },
    { min: 3, max: 25, message: 'Length should be 3 to 5', trigger: 'blur' },
  ],
  gender: [{ required: true, message: 'Please select gender', trigger: 'change' }],
})

const getTableData = async () => {
  try {
    const res = await axios.get('http://api.localhost.com/get_user_list')

    tableData.value = res.data
  } catch (error) {
    console.error(error)
  }
}

const submit = async () => {
  console.log('submit')
  if (form.id) {
    await editUser()
  } else {
    await addUser()
  }
}

const addUser = async () => {
  try {
    await axios.post('http://api.localhost.com/add_user', form)
    dialogFormVisible.value = false
    form.name = ''
    getTableData()
  } catch (error) {
    console.error(error)
  }
}

const editUser = async () => {
  try {
    await axios.put(`http://api.localhost.com/edit_user/${form.id}`, form)
    dialogFormVisible.value = false
    form.name = ''
    delete form.id
    getTableData()
  } catch (error) {
    console.error(error)
  }
}

const edit = (index: number, row: RuleForm) => {
  console.log(index, row)
  form.id = row.id
  form.name = row.name
  form.gender = row.gender
  dialogFormVisible.value = true
}

getTableData()
</script>
<template>
  <div class="prose px-3 md:px-6 prose-indigo sm:rounded-md">
    <el-button type="primary" @click="dialogFormVisible = !dialogFormVisible">add</el-button>
    <el-table :data="tableData" class="flex justify-center w-full">
      <el-table-column prop="id" label="id" min-width="80"></el-table-column>
      <el-table-column prop="name" label="name" min-width="80"></el-table-column>
      <el-table-column prop="gender" label="gender" min-width="80"></el-table-column>
      <el-table-column fixed="right" label="Operations" min-width="180">
        <template #default="scope">
          <el-button type="primary" @click="edit(scope.$index, scope.row)">Edit</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination background layout="prev, pager, next" :total="10" />
  </div>
  <el-dialog v-model="dialogFormVisible" title="add user">
    <el-form :model="form" :rules="rules">
      <el-form-item label="user name" prop=name>
        <el-input v-model="form.name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Zones" prop="gender">
        <el-select v-model="form.gender" placeholder="Please select a zone">
          <el-option label="male" value="male" />
          <el-option label="female" value="female" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="submit"> Confirm </el-button>
      </div>
    </template>
  </el-dialog>
</template>
