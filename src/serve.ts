import Koa from 'koa'
import route from './rest/item.js'

const app = new Koa()
const PORT = 8877

app.use(route.routes()).use(route.allowedMethods())

app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`)
})
