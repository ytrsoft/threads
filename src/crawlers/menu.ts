import { Page } from 'playwright'
import { PlaywrightCrawler } from 'crawlee'
import { BASE_URL, TAG_MENU, TAG_MAX } from '../utils/index.js'
import { CategoryService } from '../service/category_service.js'
import { PagerService } from '../service/pager_service.js'
import { Category, TCategory } from '../entities/category.js'

const categoryService = new CategoryService()
const pagerService = new PagerService()

const categoryRoute = async(page: Page): Promise<TCategory[]> => {
  return await page.$$eval('.forumList li', (list) => {
    const categories: TCategory[] = []
    list.forEach((li) => {
      const title = li.textContent.replace(/\s+/g, '')
      const id = li.getAttribute('fid') as string
      if (!['47', '48'].includes(id)) {
        categories.push({title, id})
      }
    })
    return categories
  })
}

const maxRoute = async(page: Page): Promise<number> => {
  const items = await page.$$('.pagination .page-item')
  if (items.length >= 2) {
    const latest = items[items.length - 2]
    const body = await latest.textContent()
    if (body) {
      const match = body.match(/\d+/)
      if (match) {
        return Number(match[0])
      }
    }
  }
  return -1
}

const genRequests = (categories: TCategory[]) => {
  return categories.map((item) => {
    return {
      label: TAG_MAX,
      url: `${BASE_URL}/forum-${item.id}.htm`,
      userData: {
        id: item.id
      }
    }
  })
}

export default async function() {
  const inst = new PlaywrightCrawler({
    async requestHandler({ request, page }) {
      if (request.label === TAG_MENU) {
        const categories = await categoryRoute(page)
        await categoryService.save(categories)
        await inst.addRequests(
          genRequests(categories)
        )
      }
      if (request.label === TAG_MAX) {
        const maxpage = await maxRoute(page)
        if (maxpage != -1) {
          const id = request.userData.id
          await pagerService.save({
            cid: id,
            pages: maxpage
          })
        }
      }
    }
  })

  await inst.addRequests([
    {
      label: TAG_MENU,
      url: `${BASE_URL}`
    }
  ])

  await inst.run()
}
