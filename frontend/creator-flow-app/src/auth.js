import axios from "axios";

async function isAuthenticated() {
    const token = localStorage.getItem('access_token');
    if (!token){
        console.log("HELLLLLLO")
        return false;
    }
    
    try{
        const response = await axios.get('/auth-check', {
            headers: {
                'Authorization': 'Bearer $(token)'
            }
        });
        const data = await response.json()
        return data.authenticated;
    } 
    catch (error) {
        console.log('Error checking authentication status: ', error)
        return false;
    }
}

export default isAuthenticated;