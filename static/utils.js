function create_signed_url(file) {
  const bucket = document.getElementById('inputBucket').value;
  let object = document.getElementById('customPath').value;
  if (object === undefined || object.length === 0) {
    object = file.name
  }
  const url = `sign?bucket=${bucket}&object=${object}`
  $.get(url, (data, status) => {
    if (status === 'success') {
      upload_to_s3(file, data);
    } else {
      return undefined;
    }
  });
}

function upload_to_s3(selected_file, data) {
  if (selected_file !== undefined) {
    const formData = new FormData();
    formData.append('Content-Type', selected_file.type);
    Object.entries(data.signed_url.fields).forEach(([k, v]) => {
      formData.append(k, v);
    });
    formData.append('acl', 'private');
    formData.append('file', selected_file);

    axios.post(data.signed_url.url, formData, {
    }).then((rsp) => {
      if (rsp.status === 204) {
        alert("Upload complete");
        document.getElementById('fileSelect').value = '';
      } else {
        alert("Presigned URL generate but upload was failed, check console log for more details");
      }
    });
  } else {
    alert("Something going wrong, the backend return unsuccessful request");
  }
}
