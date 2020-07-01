window.onload = () => {
  document.getElementById("submit").onclick = () => {
    const inputAlgorithms = document.getElementById("input-algs");
    const inputK = document.getElementById("input-k");
    const inputGraph = document.getElementById("input-graph");

    const request = {
      algorithm: inputAlgorithms.value,
      graph: inputGraph.value,
      k: inputK.value,
    };

    fetch("http://localhost:6067/request", {
      method: "POST",
      mode: "no-cors",
      headers: {
        "Content-Type": "application/json;charset=utf-8",
      },
      body: JSON.stringify(request),
    }).then((response) => {});
  };

  const updateLog = (logName, data) => {
    const log = document.getElementById(logName);
    const isScrolledToBottom =
      log.scrollHeight - log.clientHeight <= log.scrollTop + 1;

    const element = document.createElement("div");
    element.textContent = data;
    log.appendChild(element);

    if (isScrolledToBottom) {
      log.scrollTop = log.scrollHeight - log.clientHeight;
    }

    if (log.childNodes.length > 150) {
      log.removeChild(log.firstChild);
    }
  };

  const streamSource = new EventSource("/stream");
  streamSource.onmessage = (message) => updateLog("stream-log", message.data);
  streamSource.onerror = (_ev) => streamSource.close();

  const resultsSource = new EventSource("/results");
  resultsSource.onmessage = (message) => updateLog("results-log", message.data);
  resultsSource.onerror = (_ev) => resultsSource.close();
};
