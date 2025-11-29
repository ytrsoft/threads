import { createCheerioRouter } from 'crawlee'
import { AppDataSource } from './db.js'
import { Menu, Post, Image } from './entities/index.js'
import { BASE_URL, LABEL_MENU, LABEL_LIST, LABEL_DETAIL } from './config.js'

export const router = createCheerioRouter()

router.addHandler(LABEL_MENU, async ({ $, crawler, log }) => {
  log.info('抓取菜单')

  const menuRepo = AppDataSource.getRepository(Menu)
  const menuEntities: Menu[] = []
  const requests: any[] = []

  $('.forumList li').each((_, el) => {
    const $el = $(el)
    const mid = $el.attr('fid')
    const name = $el.text().trim()

    if (!mid || ['47', '48'].includes(mid)) return

    const menu = new Menu()
    menu.id = mid
    menu.name = name
    menuEntities.push(menu)

    requests.push({
      url: `${BASE_URL}/forum-${mid}-1.htm`,
      label: LABEL_LIST,
      userData: { mid }
    })
  })

  if (menuEntities.length > 0) {
    await menuRepo.save(menuEntities)
  }

  await crawler.addRequests(requests)
})

router.addHandler(LABEL_LIST, async ({ $, request, crawler, log }) => {
  const { mid } = request.userData
  log.info(`抓取列表: ${request.url}`)

  const threads = $('.list-unstyled.threadlist li')
  const detailRequests = threads.map((_, el) => {
    const tid = $(el).attr('data-tid')
    if (!tid) return null
    return {
      url: `${BASE_URL}/thread-${tid}.htm`,
      label: LABEL_DETAIL,
      userData: { mid, pid: tid }
    }
  }).get().filter(req => req !== null)

  await crawler.addRequests(detailRequests)

  const match = request.url.match(/forum-\d+-(\d+)\.htm/)

  if (match) {
    const page = parseInt(match[1], 10)
    const nextPageUrl = `${BASE_URL}/forum-${mid}-${page + 1}.htm`

    const hasNext = $('.pagination .page-item:last-child').text().includes('▶') ||
                    ($('.pagination').length > 0 && $('.pagination .next').length > 0)

    if (hasNext) {
      await crawler.addRequests([{
        url: nextPageUrl,
        label: LABEL_LIST,
        userData: { mid }
      }])
    }
  }
})

router.addHandler(LABEL_DETAIL, async ({ $, request, log }) => {
  const { pid, mid } = request.userData
  log.info(`解析详情: ${pid}`)

  const title = $('.card-thread .media-body h4').text().trim()
  const desc = $('.card-body blockquote span').text().trim()

  const cells: string[] = []
  $('.card-body tbody tr td').each((_, el) => {
    cells.push($(el).text().trim())
  })

  const post = new Post()
  post.id = pid
  post.mid = mid
  post.title = title
  post.description = desc
  post.region = cells[0] || ''
  post.age = cells[1] || ''
  post.score = cells[2] || ''
  post.price = cells[3] || ''
  post.service = cells[4] || ''
  post.wechat = cells[5] || ''
  post.qq = cells[6] || ''
  post.phone = cells[7] || ''

  const imgs: Image[] = []
  $('.card-thread img.img-fluid').each((_, el) => {
    const src = $(el).attr('src')
    if (src) {
      const img = new Image()
      img.pid = pid
      img.src = src
      imgs.push(img)
    }
  })

  await AppDataSource.getRepository(Post).save(post)

  if (imgs.length > 0) {
    await AppDataSource.getRepository(Image).save(imgs)
  }
})
