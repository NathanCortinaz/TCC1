async function ytDownload_py() {
    document.getElementById('button').textContent = 'Downloading...';
    document.getElementById('button').style.background = '#363b41';

    const link = document.getElementById('link').value;
    response = await eel.ytDownload(link)();

    if (response) {
        alert('Finished downloading! Press "Ok" to open folder.');
        eel.openFolder();
    } else {
        alert('This video is not allowed to be downloaded!');
    }

    document.getElementById('button').textContent = 'Download';
    document.getElementById('button').style.background = '#ea4c88';
}
