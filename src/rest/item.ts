import Router from 'koa-router'

const router = new Router()

router.get('/connect', async (ctx) => {
  ctx.body = { ok: 200 }
})

export default router
