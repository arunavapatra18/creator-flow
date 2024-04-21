<template>
    <div class="registration surface-card p-4 shadow-6 border-round-xl m-6 w-10">
        <h2>Welcome Back</h2>
        <form v-on:submit.prevent="handleSubmit">
            <FloatLabel class="w-full">
                <InputText class="w-full" id="email" type="email" v-model="email_value" required/>
                <label for="email">Email</label>
            </FloatLabel>
            <FloatLabel class="w-full">
                <Password input-id="password" v-model="password_value" toggleMask :feedback="false"/>
                <label for="password">Password</label>
            </FloatLabel>
            <Button type="submit" class="w-max">Sign In</Button>
            <RouterLink to="/">
                <Button label="Register" link />
            </RouterLink>
        </form>
    </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "../axios";

const email_value = ref();
const password_value = ref();

const handleSubmit = () => {
    axios.post('/login', {
        username: email_value.value,
        password: password_value.value
    },
    {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => console.log(response.status))
    .catch(error => console.log(error.response))
}

</script>
