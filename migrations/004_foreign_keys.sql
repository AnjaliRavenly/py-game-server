
--
-- Constraints for dumped tables
--

--
-- Constraints for table `heroes`
--
ALTER TABLE `heroes`
  ADD CONSTRAINT `heroes_hero_type_id_foreign` FOREIGN KEY (`hero_type_id`) REFERENCES `hero_types` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `heroes_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
