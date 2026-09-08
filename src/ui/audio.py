"""Injected browser speech recognition component."""
import streamlit as st
import streamlit.components.v1 as components

@st.cache_data(show_spinner=False)
def _mic_component(lang_code: str):
    return """<div id="mic-root" style="display:none"></div>
<script>
(function(){
  var host = window.parent.document;
  var win  = window.parent;
  var SR   = win.SpeechRecognition || win.webkitSpeechRecognition;
  if (!SR) return;

  if (!host.getElementById('th-mic-style')) {
    var s = host.createElement('style');
    s.id = 'th-mic-style';
    s.textContent = ''
      + '[data-testid="stChatInput"] form { position: relative !important; overflow: visible !important; }'
      + '[data-testid="stChatInput"] > div { overflow: visible !important; }'
      + '#th-mic-btn {'
      + '  position: absolute; right: 50px; top: 50%; transform: translateY(-50%);'
      + '  width: 32px; height: 32px; border-radius: 50%;'
      + '  border: 1.5px solid #CBD5E1; background: #FFFFFF; color: #0B6BCB;'
      + '  font-size: 15px; cursor: pointer; z-index: 99999; padding: 0;'
      + '  box-shadow: 0 1px 4px rgba(0,0,0,0.06);'
      + '  display: flex; align-items: center; justify-content: center;'
      + '  transition: background .15s, border-color .15s;'
      + '}'
      + '#th-mic-btn:hover { background: #EAF2FE; border-color: #0B6BCB; }'
      + '#th-mic-btn.listening {'
      + '  background: #DC2626; border-color: #DC2626; color: #FFFFFF;'
      + '  animation: th_pulse 1.2s infinite;'
      + '}'
      + '@keyframes th_pulse {'
      + '  0%  { box-shadow: 0 0 0 0 rgba(220,38,38,0.45); }'
      + '  70% { box-shadow: 0 0 0 10px rgba(220,38,38,0); }'
      + '  100%{ box-shadow: 0 0 0 0 rgba(220,38,38,0); }'
      + '}'
      + '#th-bubble {'
      + '  position: fixed; display: none; background: #FFFFFF; color: #0F172A;'
      + '  border: 1.5px solid #CBD5E1; border-radius: 12px;'
      + '  padding: 10px 16px; font-size: 14px; max-width: 320px;'
      + '  word-wrap: break-word;'
      + '  box-shadow: 0 8px 24px rgba(15,23,42,0.14); z-index: 999999;'
      + '}'
      + '#th-bubble.show { display: block; }';
    host.head.appendChild(s);
  }

  var btn = host.getElementById('th-mic-btn') || host.createElement('button');
  btn.id = 'th-mic-btn';
  btn.type = 'button';
  btn.innerHTML = '\U0001F399\uFE0F';
  btn.title = 'Speak your symptoms';

  var bubble = host.getElementById('th-bubble') || host.createElement('div');
  bubble.id = 'th-bubble';
  if (!bubble.parentNode) host.body.appendChild(bubble);

  var injected = false;
  function injectMic() {
    if (injected) return;
    var form = host.querySelector('[data-testid="stChatInput"] form');
    if (!form) form = host.querySelector('[data-testid="stChatInput"] > div');
    if (!form) return;
    form.appendChild(btn);
    injected = true;
    var ta = host.querySelector('[data-testid="stChatInput"] textarea');
    if (ta && ta.dataset.padded !== '1') {
      ta.dataset.padded = '1';
      ta.style.paddingRight = '88px';
    }
  }
  var injTimer = setInterval(function(){ injectMic(); if (injected) clearInterval(injTimer); }, 400);

  var listening = false, rec = null, ft = '', delivered = false;

  function deliver(t) {
    try {
      var ta = host.querySelector('[data-testid="stChatInput"] textarea');
      if (!ta) return false;
      try { Object.getOwnPropertyDescriptor(win.HTMLTextAreaElement.prototype, 'value').set.call(ta, t); }
      catch(e1) { ta.value = t; }
      ta.dispatchEvent(new Event('input', { bubbles: true }));
      ta.dispatchEvent(new Event('change', { bubbles: true }));
      setTimeout(function(){
        var sendBtn = host.querySelector('[data-testid="stChatInputSubmitButton"]');
        if (sendBtn) sendBtn.click();
      }, 400);
      return true;
    } catch (e) { return false; }
  }

  btn.onclick = function (e) {
    e.preventDefault();
    e.stopPropagation();
    if (listening) { if (rec) rec.stop(); return; }

    ft = '';
    rec = new SR();
    rec.lang = '__LANG__';
    rec.interimResults = true;
    rec.continuous = false;

    rec.onstart = function () {
      listening = true;
      btn.classList.add('listening');
      btn.innerHTML = '\u23F9';
    };

    rec.onend = function () {
      listening = false;
      btn.classList.remove('listening');
      btn.innerHTML = '\U0001F399\uFE0F';
      bubble.classList.remove('show');
      if (!delivered && ft.trim()) { delivered = true; deliver(ft.trim()); }
    };

    rec.onresult = function (ev) {
      var interim = '';
      for (var i = ev.resultIndex; i < ev.results.length; i++) {
        if (ev.results[i].isFinal) ft += ev.results[i][0].transcript;
        else interim += ev.results[i][0].transcript;
      }
      if (interim) {
        bubble.innerHTML = '\U0001F399\uFE0F ' + interim;
        bubble.classList.add('show');
        var inpRect = host.querySelector('[data-testid="stChatInput"]').getBoundingClientRect();
        bubble.style.bottom = (win.innerHeight - inpRect.top + 12) + 'px';
        bubble.style.right  = (win.innerWidth - inpRect.right + 16) + 'px';
      }
      if (ft.trim()) {
        delivered = true;
        deliver(ft.trim());
        rec.stop();
      }
    };

    rec.onerror = function () {
      listening = false;
      btn.classList.remove('listening');
      btn.innerHTML = '\U0001F399\uFE0F';
      bubble.classList.remove('show');
      if (!delivered && ft.trim()) { delivered = true; deliver(ft.trim()); }
    };

    rec.start();
  };
})();
</script>""".replace("__LANG__", lang_code or "en-IN")



def inject_mic_component(lang_code: str):
    components.html(_mic_component(lang_code), height=0)
