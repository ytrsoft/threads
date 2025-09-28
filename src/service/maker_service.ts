import _ from 'lodash'
import { Maker } from '../entities/maker.js'
import { BaseService } from './base_service.js'

export class MakerService extends BaseService<Maker> {
  constructor() {
    super(Maker)
  }
}
