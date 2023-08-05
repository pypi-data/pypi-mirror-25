/*
 * Copyright (C) Pootle contributors.
 *
 * This file is a part of the Pootle project. It is distributed under the GPL3
 * or later license. See the LICENSE file for a copy of the license and the
 * AUTHORS file for copyright and authorship information.
 */

import { User, UserSet } from 'models/user';
import UserController from './UserController';


export default {
  Controller: UserController,
  Model: User,
  Collection: UserSet,
};
