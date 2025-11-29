import 'reflect-metadata'
import { CheerioCrawler } from 'crawlee'
import { router } from './routes.js'
import { initDB } from './db.js'
import { BASE_URL, LABEL_MENU } from './config.js'

const main = async () => {
  await initDB()

  const crawler = new CheerioCrawler({
    requestHandler: router,
    maxConcurrency: 10,
    minConcurrency: 2,
    maxRequestRetries: 2,
    requestHandlerTimeoutSecs: 60
  })

  await crawler.run([{
    url: BASE_URL,
    label: LABEL_MENU
  }])
}

main()
