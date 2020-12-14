import { request, request1 } from './request'

export function getHomeMultidata () {
  return request({
    url: '/course/filelist'
  })
}

export function postHomeMultidata (id) {
  return request({
    url: '/course/upvote',
    method: 'post',
    data: id
  })
}

export function postRegister (myname, mypassword) {
  return request1({
    url: '/user/signup',
    method: 'post',
    data: {
      name: myname,
      password: mypassword,
      email: '12345678@pku.edu.cn'
    }
  })
}
