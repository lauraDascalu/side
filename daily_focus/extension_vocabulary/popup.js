(async () => {
  const data = await chrome.storage.local.get(['userLevel', 'userHour', 'userMinute']);
  
  if (data.userLevel) document.getElementById('level-select').value = data.userLevel;
  if (data.userHour) document.getElementById('hour-select').value = data.userHour;
  if (data.userMinute) document.getElementById('minute-select').value = data.userMinute;

  document.getElementById('save-settings').addEventListener('click', async () => {
    const level = document.getElementById('level-select').value;
    const hour = parseInt(document.getElementById('hour-select').value);
    const minute = parseInt(document.getElementById('minute-select').value);

    await chrome.storage.local.set({ 
      userLevel: level, 
      userHour: hour, 
      userMinute: minute 
    });

    chrome.runtime.sendMessage({ action: "updateSettings" });

    const status = document.getElementById('status-msg');
    status.textContent = "Next notification will show up at set time.";
    setTimeout(() => { status.textContent = ""; }, 3000);
  });
})();