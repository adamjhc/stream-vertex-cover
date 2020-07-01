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

  const streamSource = new EventSource("/stream");
  streamSource.onmessage = (message) => {
    const streamLog = document.getElementById("stream-log");
    const isScrolledToBottom =
      streamLog.scrollHeight - streamLog.clientHeight <=
      streamLog.scrollTop + 1;

    const element = document.createElement("div");
    element.textContent = message.data;
    streamLog.appendChild(element);

    if (isScrolledToBottom) {
      streamLog.scrollTop = streamLog.scrollHeight - streamLog.clientHeight;
    }

    if (streamLog.childNodes.length > 100) {
      streamLog.removeChild(streamLog.firstChild);
    }
  };
  streamSource.onerror = (_ev) => {
    streamSource.close();
  };

  const resultsSource = new EventSource("/results");
  resultsSource.onmessage = (message) => {
    const streamLog = document.getElementById("results-log");
    const isScrolledToBottom =
      streamLog.scrollHeight - streamLog.clientHeight <=
      streamLog.scrollTop + 1;

    const element = document.createElement("div");
    element.textContent = message.data;
    streamLog.appendChild(element);

    if (isScrolledToBottom) {
      streamLog.scrollTop = streamLog.scrollHeight - streamLog.clientHeight;
    }

    if (streamLog.childNodes.length > 100) {
      streamLog.removeChild(streamLog.firstChild);
    }
  };
  resultsSource.onerror = (_ev) => {
    resultsSource.close();
  };
};
