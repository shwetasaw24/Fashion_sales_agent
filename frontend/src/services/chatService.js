import axios from "axios"

export async function sendChat(payload) {
  const { data } = await axios.post(
    "http://localhost:8000/chat",
    payload
  )
  return data
}
