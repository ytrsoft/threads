import _ from 'lodash'
import { Maker } from '../entities/marker.js'
import { BaseService } from './base_service.js'

export class MarkerService extends BaseService<Maker> {
  constructor() {
    super(Maker)
  }
}
