import { Page } from 'playwright'
import { PlaywrightCrawler } from 'crawlee'
import { BASE_URL } from '../utils/index.js'
import { PagerService } from '../service/pager_service.js'
import { MarkerService } from '../service/maker_service.js'
import { TMaker } from '../entities/marker.js'

const pagerService = new PagerService()
const markerService = new MarkerService()

const itemRoute = async(cid: string, page: Page): Promise<TMaker[]> => {
  const pids = await page.$$eval('.list-unstyled.threadlist li', (list) => {
    return list.map((li) => {
      return li.getAttribute('data-tid') as string
    })
  })
  return pids.map((pid) => {
    return { cid, pid }
  })
}

export default async function() {
  const inst = new PlaywrightCrawler({
    async requestHandler({ request, page }) {
      const { pager } = request.userData.entity
      const marks = await itemRoute(
        pager.cid, page
      )
      markerService.save(marks)
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
