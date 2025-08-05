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
        margin: 0; height: 100%;
        display: flex; justify-content: center; align-items: center;
        background: #111; color: #fff;
        font-family: sans-serif;
      }
      canvas {
        border-radius: 50%;
        background: #222;
      }
    </style>
  </head>
  <body>
    <canvas id="waterBall" width="300" height="300"></canvas>
    <script>
      const canvas = document.getElementById('waterBall')
      const ctx = canvas.getContext('2d')
      const radius = 150
      let percent = 0
      let waveOffset = 0

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

      function animate() {
        waveOffset += 2
        drawWaterBall(percent)
        requestAnimationFrame(animate)
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

      setInterval(fetchProgress, 1000)
      fetchProgress()
      animate()
    </script>
  </body>
  </html>
  `
})

export default router
