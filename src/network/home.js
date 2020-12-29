import { request } from './request'

export function getFilelist () {
  return request({
    url: '/course/filelist',
    method: 'get'
  })
}

export function getMaterials (datas) {
  return request({
    url: '/course/download/',
    method: 'post',
    data: datas
  })
}

export function postMaterials (datas) {
  return request({
    url: '/course/upload/',
    method: 'post',
    data: datas
  })
}

export function postFilelist (id) {
  return request({
    url: '/course/upvote/',
    method: 'post',
    data: id
  })
}

export function postRegister (datas) {
  return request({
    url: '/user/test_init',
    method: 'post',
    data: datas
  })
}

export function postLogin (datas) {
  return request({
    url: '/user/login',
    method: 'post',
    data: datas
  })
}

export function getddl (datas) {
  return request({
    url: '/schedule/getdeadlinescalendar',
    method: 'post',
    data: datas
  })
}

export function addddl (datas) {
  return request({
    url: '/schedule/addschedule',
    method: 'post',
    data: datas
  })
}

export function delddl (datas) {
  return request({
    url: '/schedule/deleteschedule',
    method: 'post',
    data: datas
  })
}
