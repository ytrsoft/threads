import { Page } from 'playwright'
import { PlaywrightCrawler } from 'crawlee'
import { BASE_URL } from '../utils/index.js'
import { PageService } from '../service/page_service.js'
import { FlagService } from '../service/flag_service.js'
import { Flag } from '../entities/flag.js'

const pageService = new PageService()
const flagService = new FlagService()

const itemRoute = async(cid: string, page: Page): Promise<Partial<Flag>[]> => {
  return await page.$$eval('.list-unstyled.threadlist li', (list) => {
    const items: Partial<Flag>[] = []
    list.forEach((li) => {
      const pid = li.getAttribute('data-tid') as string
      items.push({ cid, pid })
    })
    return items
  })
}

export default async function() {
  const inst = new PlaywrightCrawler({
    async requestHandler({ request, page }) {
      const entity = request.userData.entity
      const flags = await itemRoute(
        entity.page.cid, page
      )
      flagService.save(flags)
      pageService.visited(entity.page)
    }
  })

  const pages = await pageService.query()

  const requests = pages.map((page) => {
    return {
      userData: {
        entity: {
          page
        }
      },
      url: `${BASE_URL}/forum-${page.cid}-${page.page}.htm?orderby=lastpid&digest=0`
    }
  })

  await inst.addRequests(requests)

  await inst.run()
}
