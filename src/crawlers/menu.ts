import { Page } from 'playwright'
import { PlaywrightCrawler } from 'crawlee'
import { BASE_URL, TAG_MENU, TAG_MAX } from '../utils/index.js'
import { saveMenus } from '../service/data_service.js'
import { Menu } from '../entities/menu.js'

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

export default async function() {
  const inst = new PlaywrightCrawler({
    async requestHandler({ request, page }) {
      if (request.label === TAG_MENU) {
        const list = await menuRoute(page)
        await saveMenus(list)
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
