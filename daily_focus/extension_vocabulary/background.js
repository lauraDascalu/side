function calcDateStart(ora, minut) {
  const acum = new Date();
  const start = new Date();
  start.setHours(ora, minut, 0, 0);
  
  if (acum > start) {
    start.setDate(start.getDate() + 1);
  }
  return start.getTime();
}

async function setupAlarm() {
  const data = await chrome.storage.local.get(['userHour', 'userMinute']);
  // default
  const h = data.userHour !== undefined ? data.userHour : 9;
  const m = data.userMinute !== undefined ? data.userMinute : 0;

  chrome.alarms.clear("dailyWordUpdate", () => {
    const timpStart = calcDateStart(h, m);
    chrome.alarms.create("dailyWordUpdate", { 
      when: timpStart, 
      periodInMinutes: 1440 // 24h
    });
    console.log('Alarm set for: ${h}:${m}');
  });
}

async function updateDailyWord() {
  try {
    const data = await chrome.storage.local.get(['userLevel']);
    if (!data.userLevel) return;

    const response = await fetch(chrome.runtime.getURL('data.json'));
    const words = await response.json();
    const filteredWords = words.filter(w => w.level === data.userLevel);
    
    if (filteredWords.length === 0) return;
    const newWord = filteredWords[Math.floor(Math.random() * filteredWords.length)];

    chrome.notifications.create({
      type: "list",
      iconUrl: "icons/icon128.png",
      title: newWord.word,
      message: "Today's word",
      items:[
        {title: "Definition", message: newWord.def},
        {title: "Example", message: newWord.ex}
      ],
      priority: 2,
      requireInteraction: true
    });
  } catch (error) {
    console.error("Error:", error);
  }
}

chrome.runtime.onInstalled.addListener(() => {
  setupAlarm();
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "updateSettings") {
    setupAlarm();
    sendResponse({ status: "success" });
  }
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "dailyWordUpdate") {
    updateDailyWord();
  }
});
