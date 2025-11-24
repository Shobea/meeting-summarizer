// src/composables/useNfcSocket.js
import { ref, onMounted, onBeforeUnmount } from "vue";

export function useNfcSocket(wsUrl) {
  const socket = ref(null);
  const lastScan = ref(null); // { nfc_id, reader_id, timestamp }
  const connected = ref(false);

  function connect() {
    socket.value = new WebSocket(wsUrl);

    socket.value.onopen = () => {
      connected.value = true;
      console.log("WebSocket connected");
    };

    socket.value.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data);
        if (data?.uid) {
        lastScan.value = {
            nfc_id: data.uid,      // use uid from Android
            reader_id: data.reader_id || null,
            timestamp: Date.now(), // add timestamp client-side
        };
        console.log("Scan received:", lastScan.value);
        }

      } catch (e) {
        console.error("WS parse error", e);
      }
    };

    socket.value.onclose = () => {
      connected.value = false;
      console.log("WebSocket closed, reconnect in 2s");
      setTimeout(connect, 2000);
    };

    socket.value.onerror = (err) => {
      console.error("WebSocket error", err);
      socket.value.close();
    };
  }

  onMounted(connect);
  onBeforeUnmount(() => {
    if (socket.value) socket.value.close();
  });

  return { lastScan, connected };
}
