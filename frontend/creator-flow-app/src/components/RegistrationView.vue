<template>
    <div class="form bg-teal-300 border-round-2xl shadow-8">
        <div class="registration surface-card p-4 shadow-6 border-round-xl m-6 w-10">
            <h2>Create Account</h2>
            <form v-on:submit.prevent="handleSubmit">
                <FloatLabel class="w-full">
                    <InputText class="w-full" id="name" type="text" v-model="name_value" required/>
                    <label for="name">Name</label>
                </FloatLabel>
                <FloatLabel class="w-full">
                    <InputText class="w-full" id="email" type="email" v-model="email_value" required/>
                    <label for="email">Email</label>
                </FloatLabel>
                <FloatLabel class="w-full">
                    <Password input-id="password" v-model="password_value" toggleMask  required promptLabel="Choose a password"
                        weakLabel="Too simple" mediumLabel="Average complexity" strongLabel="Complex password" />
                    <label for="password">Password</label>
                </FloatLabel>
                <Dropdown class="w-full" v-model="selectedRole" :options="roles" placeholder="Select a Role" checkmark />
                <Button type="submit" class="w-max" label="Create an Account" />
                <RouterLink to="/sign-in">
                    <Button label="Sign In" link />
                </RouterLink>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from '../axios'

const name_value = ref();
const email_value = ref();
const password_value = ref();
const selectedRole = ref();

const roles = ref(['CREATOR', 'EDITOR']);
/**
 * 
 */
const handleSubmit = () => {
    axios.post('/register',{
        name: name_value.value,
        email: email_value.value,
        role: selectedRole.value,
        password: password_value.value
    })
    .then(response => console.log(response.status))
    .catch(error => console.log(error.response))
}

</script>
