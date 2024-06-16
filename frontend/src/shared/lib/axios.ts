import axios from "axios";
const instance = axios.create({
  baseURL: process.env["NEXT_PUBLIC_BACKEND_URL"],
  timeout: 5000
})

export default instance