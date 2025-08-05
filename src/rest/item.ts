import Router from 'koa-router'
import sqlite from '../sqlite/index.js'

const router = new Router()

router.get('/item/rate', async (ctx) => {
  const result = await sqlite.query(`
    SELECT
      CASE
        WHEN (SELECT COUNT(fid) FROM item) = 0 THEN 0
        ELSE (SELECT COUNT(fid) FROM item WHERE visited = 1) * 100
             / (SELECT COUNT(fid) FROM item)
      END AS rate
  `)
  const rate = result[0].rate ?? 0
  ctx.body = { progress: rate }
})

router.get('/item/dist', async (ctx) => {
  const result = await sqlite.query(`
      SELECT menu.label, menu.fid, COUNT(detail.fid) AS total
        FROM detail
          JOIN menu ON detail.fid = menu.fid
              GROUP BY menu.label
      ORDER BY total DESC
  `)
  ctx.body = result
})

router.get('/item/result', async (ctx) => {
  ctx.type = 'html'
  ctx.body = `
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>抓取进度</title>
    <style>
      html, body {
        margin: 0;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        background: #121212;
        font-family: 'Arial', sans-serif;
        color: #fff;
      }
      .container {
        display: flex;
        justify-content: space-around;
        width: 100%;
        max-width: 1000px;
        align-items: center;
        padding: 20px;
        gap: 40px;
      }
      .progress-container {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
      }
      .dist-container {
        flex: 1;
        max-width: 320px;
        padding: 20px;
        background: #222;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
      }
      canvas {
        border-radius: 50%;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
      }
      .dist-item {
        margin-bottom: 15px;
        font-size: 16px;
        font-weight: 500;
        color: #ddd;
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
      }
      .dist-item span {
        color: #4caf50;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="progress-container">
        <canvas id="waterBall" width="300" height="300"></canvas>
      </div>
      <div class="dist-container">
        <div id="distData"></div>
      </div>
    </div>
    <script>
      const canvas = document.getElementById('waterBall')
      const ctx = canvas.getContext('2d')
      const radius = 150
      let percent = 0
      let waveOffset = 0
      let distData = []

      function drawWaterBall(p) {
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        ctx.beginPath()
        ctx.arc(radius, radius, radius - 5, 0, Math.PI * 2)
        ctx.strokeStyle = '#4caf50'
        ctx.lineWidth = 5
        ctx.stroke()

        const waterLevel = radius * 2 * (1 - p / 100)
        const waveHeight = 10
        const waveLength = 50

        ctx.beginPath()
        ctx.moveTo(0, canvas.height)
        for (let x = 0; x <= canvas.width; x++) {
          const y = waveHeight * Math.sin((x + waveOffset) / waveLength * Math.PI * 2) + waterLevel
          ctx.lineTo(x, y)
        }
        ctx.lineTo(canvas.width, canvas.height)
        ctx.closePath()
        ctx.fillStyle = '#4caf50aa'
        ctx.fill()

        ctx.font = 'bold 36px sans-serif'
        ctx.fillStyle = '#fff'
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        ctx.fillText(p + '%', radius, radius)
      }

      async function fetchProgress() {
        try {
          const res = await fetch('/item/rate')
          const data = await res.json()
          percent = Math.min(Math.max(parseInt(data.progress), 0), 100)
        } catch (err) {
          console.error('请求失败', err)
        }
      }

      async function fetchDistData() {
        try {
          const res = await fetch('/item/dist')
          distData = await res.json()
          updateDistData()
        } catch (err) {
          console.error('请求失败', err)
        }
      }

      function updateDistData() {
        const distContainer = document.getElementById('distData')
        distContainer.innerHTML = ''
        distData.forEach(item => {
          const div = document.createElement('div')
          div.classList.add('dist-item')
          div.innerHTML = '<span>' + item.label + '</span> ' + item.total
          distContainer.appendChild(div)
        })
      }

      function animate() {
        waveOffset += 2
        drawWaterBall(percent)
        requestAnimationFrame(animate)
      }

      setInterval(() => {
        fetchProgress()
        fetchDistData()
      }, 1000)

      fetchProgress()
      fetchDistData()
      animate()
    </script>
  </body>
  </html>
  `
})


export default router
