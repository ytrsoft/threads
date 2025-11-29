import 'reflect-metadata'
import Koa from 'koa'
import Router from '@koa/router'
import bodyParser from 'koa-bodyparser'
import cors from '@koa/cors'
import views from 'koa-views'
import path from 'path'
import { fileURLToPath } from 'url'
import { Brackets } from 'typeorm'
import { AppDataSource, initDB } from './db.js'
import { Post, Menu, Image } from './entities/index.js'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const app = new Koa()
const router = new Router()

app.use(cors())
app.use(bodyParser())
app.use(views(path.join(__dirname, 'views'), { extension: 'ejs' }))

router.get('/menus', async (ctx) => {
  try {
    const sql = `
      SELECT m.id, m.name, COUNT(p.id) AS value
      FROM menu AS m
      LEFT JOIN post AS p ON p.mid = m.id
      GROUP BY m.id, m.name
      HAVING value > 0
      ORDER BY value DESC;
    `
    const result = await AppDataSource.query(sql)
    ctx.body = { code: 0, data: result }
  } catch (err) {
    ctx.status = 500
    ctx.body = { code: 500, message: 'Error' }
  }
})

router.get('/posts', async (ctx) => {
  try {
    const mid = ctx.query.mid as string
    const kw = ctx.query.kw as string || ''
    const page = parseInt(ctx.query.page as string) || 1
    const pageSize = parseInt(ctx.query.pageSize as string) || 20

    if (!mid) {
      ctx.status = 400
      ctx.body = { code: 400, message: 'Missing mid' }
      return
    }

    const qb = AppDataSource.getRepository(Post).createQueryBuilder('post')
    qb.where('post.mid = :mid', { mid })

    if (kw.trim()) {
      const likeKw = `%${kw.trim()}%`
      qb.andWhere(new Brackets(innerQb => {
        innerQb.where('post.title LIKE :kw', { kw: likeKw })
          .orWhere('post.description LIKE :kw', { kw: likeKw })
          .orWhere('post.region LIKE :kw', { kw: likeKw })
          .orWhere('post.age LIKE :kw', { kw: likeKw })
          .orWhere('post.score LIKE :kw', { kw: likeKw })
          .orWhere('post.price LIKE :kw', { kw: likeKw })
          .orWhere('post.service LIKE :kw', { kw: likeKw })
          .orWhere('post.wechat LIKE :kw', { kw: likeKw })
          .orWhere('post.phone LIKE :kw', { kw: likeKw })
      }))
    }

    qb.orderBy('post.id', 'DESC')
      .skip((page - 1) * pageSize)
      .take(pageSize)

    const [list, total] = await qb.getManyAndCount()

    ctx.body = {
      code: 0,
      data: { list, total, page, pageSize, totalPage: Math.ceil(total / pageSize) }
    }
  } catch (err) {
    ctx.status = 500
    ctx.body = { code: 500, message: 'Error' }
  }
})

router.get('/', async (ctx) => {
  try {
    const mid = ctx.query.mid as string
    const kw = ctx.query.kw as string || ''
    const sortBy = ctx.query.sortBy as string || 'id'
    const order = (ctx.query.order as string || 'DESC').toUpperCase() as 'ASC' | 'DESC'
    const page = parseInt(ctx.query.page as string) || 1
    const pageSize = 24

    const menus = await AppDataSource.query(`
      SELECT m.id, m.name, COUNT(p.id) as count
      FROM menu m
      LEFT JOIN post p ON p.mid = m.id
      GROUP BY m.id HAVING count > 0
      ORDER BY count DESC
    `)

    const qb = AppDataSource.getRepository(Post).createQueryBuilder('post')

    if (mid) {
      qb.where('post.mid = :mid', { mid })
    }

    if (kw.trim()) {
      const likeKw = `%${kw.trim()}%`
      qb.andWhere(new Brackets(innerQb => {
        innerQb.where('post.title LIKE :kw', { kw: likeKw })
          .orWhere('post.region LIKE :kw', { kw: likeKw })
          .orWhere('post.service LIKE :kw', { kw: likeKw })
      }))
    }

    if (sortBy === 'price') {
      qb.orderBy('CAST(post.price AS UNSIGNED)', order)
    } else if (sortBy === 'age') {
      qb.orderBy('CAST(post.age AS UNSIGNED)', order)
    } else {
      qb.orderBy('post.id', 'DESC')
    }

    qb.skip((page - 1) * pageSize)
      .take(pageSize)

    const [posts, total] = await qb.getManyAndCount()

    for (const post of posts) {
      const img = await AppDataSource.getRepository(Image).findOne({ where: { pid: post.id } })
      Object.assign(post, { cover: img ? img.src : null })
    }

    await ctx.render('index', {
      menus,
      posts,
      currentMid: mid,
      kw,
      sortBy,
      order,
      pagination: {
        page,
        total,
        totalPage: Math.ceil(total / pageSize)
      }
    })
  } catch (err) {
    ctx.status = 500
    ctx.body = 'Server Error'
  }
})

router.get('/thread/:id', async (ctx) => {
  try {
    const { id } = ctx.params
    const post = await AppDataSource.getRepository(Post).findOneBy({ id })

    if (!post) {
      ctx.status = 404
      return
    }

    const images = await AppDataSource.getRepository(Image).find({ where: { pid: id } })

    await ctx.render('detail', { post, images })
  } catch (err) {
    ctx.status = 500
    ctx.body = 'Server Error'
  }
})

const startServer = async () => {
  await initDB()
  app.use(router.routes()).use(router.allowedMethods())
  app.listen(3000, () => {
    console.log('🚀 Server running at http://localhost:3000')
  })
}

startServer()
