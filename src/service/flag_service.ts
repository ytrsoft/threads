import _ from 'lodash'
import sqlite from '../sqlite/index.js'
import { Flag } from '../entities/flag.js'

export class FlagService {

  protected repo = sqlite.getRepository(Flag)

  async save(flag: Partial<Flag>[]): Promise<Flag[]> {
    return this.repo.save(flag)
  }

  async query(): Promise<Flag[]> {
    return this.repo.find({where: { visited: false}})
  }

  async visited(flag: Flag) {
    flag.visited = true
    await this.repo.save(flag)
  }

}
