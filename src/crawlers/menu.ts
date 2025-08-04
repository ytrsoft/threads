import { Page } from 'playwright'
import { PlaywrightCrawler } from 'crawlee'
import { BASE_URL, TAG_MENU, TAG_MAX } from '../utils/index.js'
import { saveMenus, saveFlag } from '../service/data_service.js'
import { Menu } from '../entities/menu.js'
import { Flag } from '../entities/flag.js'

const menuRoute = async(page: Page): Promise<Menu[]> => {
  return await page.$$eval('.forumList li', (list) => {
    const items: Menu[] = []
    list.forEach((li) => {
      const label = li.textContent.replace(/\s+/g, '')
      const fid = li.getAttribute('fid') as string
      if (!['47', '48'].includes(fid)) {
        items.push({label, fid} as Menu)
      }
    })
    return items
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

const genRequests = (menus: Menu[]) => {
  return menus.map((item) => {
    return {
      label: TAG_MAX,
      url: `${BASE_URL}/forum-${item.fid}.htm`,
      userData: {
        fid: item.fid
      }
    }
  })
}

export default async function() {
  const inst = new PlaywrightCrawler({
    async requestHandler({ request, page }) {
      if (request.label === TAG_MENU) {
        const list = await menuRoute(page)
        await saveMenus(list)
        await inst.addRequests(
          genRequests(list)
        )
      }
      if (request.label === TAG_MAX) {
        const pages = await maxRoute(page)
        if (pages != -1) {
          const fid = request.userData.fid
          await saveFlag({ fid, pages } as Flag)
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
