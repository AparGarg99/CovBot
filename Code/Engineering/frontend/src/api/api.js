export const postMsg = (params) => {
  console.log('postMsg', JSON.stringify(params))
    return fetch('/api/send_msg', {
        body: JSON.stringify(params),
        headers: {
          'content-type': 'application/json'
        },
        method: 'POST',
      })
        .then((res) => {
            return res.json()
        })
        .catch(e => console.error(e))
}

export const uploadAudio = (params) => {
  let formData = new FormData
  formData.append('file', params.audio)
  
  return fetch('/api/upload_audio', {
      method: 'POST',  
      body: formData,
    })
      .then((res) => {
          return res.json()
      })
      .catch(e => console.error(e))
}

export const translate = (params) => {
  return fetch('/api/translate', {
    body: JSON.stringify(params),
    headers: {
      'content-type': 'application/json'
    },
    method: 'POST',
  })
    .then((res) => {
        return res.json()
    })
    .catch(e => console.error(e))
}