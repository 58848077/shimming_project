import React, { useState } from 'react'
import axios from 'axios'
import './App.css'

const baseUrl = 'http://localhost:8000/'

function App() {
  const [url, setUrl] = useState('')
  const initApiResponse = {
    status: '',
    message: '',
    streamStatus: '',
  }
  const [apiResponse, setApiResponse] = useState(initApiResponse)
  const streamStatusReference = {
    true: '直播中',
    false: '未直播',
  }
  const errorReference = {
    url_required: '請輸入想要查詢Youtube直播網址。',
    unsupported_url: '網址錯誤或非Youtube網址。',
    api_error: '發生錯誤，請聯絡工作人員。',
  }

  const handleUrlChange = (event) => {
    setUrl(event.target.value)
  }

  async function CheckStreamStatus(url) {
    await axios.get(
      `${baseUrl}apis/stream/status/`,
      {
        params: {
          url,
        }
      }
    ).then((response) => {
      setApiResponse({
        status: response.data.status,
        streamStatus: response.data.data.stream_status,
      })
    }).catch((error) => {
      setApiResponse({
        status: error.response.data.status,
        message: error.response.data.message,
      })
    })
  }

  const handleCheckStatus = () => {
    CheckStreamStatus(url)
  }

  return (
    <div className="App">
      <div>
        <label>
          輸入想要查詢直播狀態的網址:
          <input type="text" value={url} onChange={handleUrlChange} />
        </label>
        <button onClick={handleCheckStatus}>Check Status</button>
        {apiResponse.status ? (
          <div>
            直播狀態：{streamStatusReference[apiResponse.streamStatus]}
          </div>) : (
          <div>
            {errorReference[apiResponse.message]}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
