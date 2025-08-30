// 更新时间
function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('zh-CN', {
        hour: '2-digit',
        minute: '2-digit'
    });
    document.getElementById('current-time').textContent = timeString;
}

// 每秒更新时间
setInterval(updateTime, 1000);
updateTime();

// 导航栏交互
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', function() {
        // 移除所有active类
        document.querySelectorAll('.nav-item').forEach(nav => {
            nav.classList.remove('active');
        });
        // 添加active类到当前项
        this.classList.add('active');
    });
});

// 卡片点击效果
document.querySelectorAll('.course-card').forEach(card => {
    card.addEventListener('click', function() {
        this.style.transform = 'scale(0.98)';
        setTimeout(() => {
            this.style.transform = '';
        }, 150);
    });
});

// 添加页面加载动画
window.addEventListener('load', function() {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// 添加滚动效果
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const parallax = document.querySelector('.focus-area');
    const speed = scrolled * 0.5;
    
    if (parallax) {
        parallax.style.transform = `translateY(${speed}px)`;
    }
});

// 添加触摸反馈
document.addEventListener('touchstart', function() {}, {passive: true});

// 课程卡片悬停效果增强
document.querySelectorAll('.course-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-4px) scale(1.02)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// 状态栏电池电量模拟
function updateBatteryLevel() {
    const batteryIcon = document.querySelector('.battery-icon');
    const levels = [20, 40, 60, 80, 100];
    const currentLevel = levels[Math.floor(Math.random() * levels.length)];
    
    batteryIcon.style.background = `linear-gradient(45deg, 
        ${currentLevel > 20 ? '#d4af37' : '#e74c3c'}, 
        ${currentLevel > 20 ? '#f4d03f' : '#c0392b'})`;
}

// 每30秒更新一次电池电量
setInterval(updateBatteryLevel, 30000);
updateBatteryLevel();

// ====== MathJax 渲染辅助：等待加载完成再渲染，避免出现原始 $$...$$ 文本 ======
function typesetWithMathJax(el, retry = 0) {
    if (!el) return;
    const MAX_RETRY = 20; // 最多等待约2秒（20*100ms）
    if (window.MathJax && window.MathJax.startup && window.MathJax.typesetPromise) {
        // 若有旧的 Jax，先清除再渲染
        if (typeof window.MathJax.typesetClear === 'function') {
            try { window.MathJax.typesetClear([el]); } catch (e) {}
        }
        // 确保 MathJax 完全就绪
        const p = window.MathJax.startup.promise || Promise.resolve();
        p.then(() => window.MathJax.typesetPromise([el])).catch(() => {
            // 少量失败重试
            if (retry < MAX_RETRY) setTimeout(() => typesetWithMathJax(el, retry + 1), 100);
        });
        return;
    }
    if (retry < MAX_RETRY) setTimeout(() => typesetWithMathJax(el, retry + 1), 100);
}

// ====== 新增：从后端加载一条内容并渲染 Markdown / LaTeX / 图表 ======
async function fetchOneMLContent() {
    try {
        // 直接取后端的机器学习内容，如果没有会返回空数组
        const resp = await fetch('http://127.0.0.1:8001/api/v1/content/?module=ml&limit=1');
        if (!resp.ok) throw new Error('获取内容失败');
        const data = await resp.json();
        if (!Array.isArray(data) || data.length === 0) {
            // 回退：尝试按 math 模块获取
            const respMath = await fetch('http://127.0.0.1:8001/api/v1/content/?module=math&limit=1');
            const dataMath = await respMath.json();
            return Array.isArray(dataMath) && dataMath.length ? dataMath[0] : null;
        }
        return data[0];
    } catch (e) {
        console.error(e);
        return null;
    }
}

function renderMarkdown(md) {
    const el = document.getElementById('mdContainer');
    if (!el) return;
    const html = window.marked ? window.marked.parse(md || '') : (md || '');
    el.innerHTML = html;
}

function renderFormulas(formulas) {
    const el = document.getElementById('formulaContainer');
    if (!el) return;
    if (!formulas || typeof formulas !== 'object') {
        el.textContent = '无公式数据';
    } else {
        // 将每个公式以块级 $$...$$ 方式展示；兼容字符串或对象 {latex, explanation, symbols}
        el.innerHTML = Object.entries(formulas).map(([k, v]) => {
            const obj = (v && typeof v === 'object') ? v : { latex: String(v || '') };
            const latex = obj.latex || '';
            const explanation = obj.explanation || '';
            const symbols = (obj.symbols && typeof obj.symbols === 'object') ? obj.symbols : null;
            const symbolsHtml = symbols && Object.keys(symbols).length
                ? `<div style="margin-top:6px;">
                     <div style="color:#95a5a6;font-size:12px;">符号表</div>
                     <ul style="margin:4px 0 0 16px;padding:0;list-style:disc;color:#2c3e50;font-size:12px;">
                       ${Object.entries(symbols).map(([sk, sv]) => `<li><span style="font-family: 'Latin Modern Math', 'Times New Roman', serif;">${sk}</span>：${sv}</li>`).join('')}
                     </ul>
                   </div>`
                : '';
            return `
            <div style="margin:10px 0;padding:8px;border:1px solid rgba(212,175,55,0.25);border-radius:8px;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,0.05);">
              <div style="color:#7f8c8d;font-size:12px;margin-bottom:4px;">${k}</div>
              <div>$$${latex}$$</div>
              ${explanation ? `<div style="margin-top:6px;color:#34495e;font-size:13px;line-height:1.5;">${explanation}</div>` : ''}
              ${symbolsHtml}
            </div>`;
        }).join('');
    }
    // 关键：等待 MathJax 就绪后再 typeset，避免直接看到 $$...$$
    typesetWithMathJax(el);
}

function renderCharts(charts) {
    const el = document.getElementById('chartsContainer');
    if (!el) return;
    el.innerHTML = '';
    if (!charts || typeof charts !== 'object' || Object.keys(charts).length === 0) {
        el.textContent = '无图表数据';
        return;
    }
    Object.entries(charts).forEach(([name, imgBase64]) => {
        const card = document.createElement('div');
        card.style.border = '1px solid rgba(212,175,55,0.3)';
        card.style.borderRadius = '8px';
        card.style.padding = '8px';
        card.style.background = '#fff';
        card.style.boxShadow = '0 2px 8px rgba(0,0,0,0.06)';

        const cap = document.createElement('div');
        cap.style.fontSize = '12px';
        cap.style.color = '#7f8c8d';
        cap.style.marginBottom = '6px';
        cap.textContent = name;

        const img = document.createElement('img');
        img.style.maxWidth = '360px';
        img.style.height = 'auto';
        // charts_data 里是纯 base64（不带 data:image/png;base64, 前缀），因此需要补齐
        img.src = imgBase64.startsWith('data:') ? imgBase64 : `data:image/png;base64,${imgBase64}`;
        img.alt = name;

        card.appendChild(cap);
        card.appendChild(img);
        el.appendChild(card);
    });
}

async function handleLoadDemo() {
    const btn = document.getElementById('load-demo-btn');
    if (!btn) return;
    btn.disabled = true;
    btn.textContent = '加载中...';
    const content = await fetchOneMLContent();
    if (!content) {
        renderMarkdown('# 没有可用的数据\n请先调用后端初始化接口 /api/v1/content/init_ml');
        renderFormulas(null);
        renderCharts(null);
        btn.disabled = false;
        btn.textContent = '加载后端示例数据';
        return;
    }
    renderMarkdown(content.content_body || '');
    renderFormulas(content.formulas || {});
    renderCharts(content.charts_data || {});
    btn.disabled = false;
    btn.textContent = '重新加载';
}

window.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('load-demo-btn');
    if (btn) btn.addEventListener('click', handleLoadDemo);
});
