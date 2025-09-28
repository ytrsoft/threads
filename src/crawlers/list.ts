import { Page } from 'playwright'
import { PlaywrightCrawler } from 'crawlee'
import { BASE_URL } from '../utils/index.js'
import { PagerService } from '../service/pager_service.js'
import { MakerService } from '../service/maker_service.js'
import { TMaker } from '../entities/maker.js'

const pagerService = new PagerService()
const makerService = new MakerService()

const itemRoute = async(cid: string, page: Page): Promise<TMaker[]> => {
  return await page.$$eval('.list-unstyled.threadlist li', (list) => {
    const items: TMaker[] = []
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
      const { pager } = request.userData.entity
      const flags = await itemRoute(
        pager.cid, page
      )
      makerService.save(flags)
      pagerService.visited(pager)
    }
  })

  const pages = await pagerService.queries()

  const requests = pages.map((pager) => {
    return {
      userData: {
        entity: {
          pager
        }
      },
      url: `${BASE_URL}/forum-${pager.cid}-${pager.page}.htm?orderby=lastpid&digest=0`
    }
  })

  await inst.addRequests(requests)

  await inst.run()
}
