import Adw from 'gi://Adw';
import Gtk from 'gi://Gtk';

import {ExtensionPreferences} from 'resource:///org/gnome/Shell/Extensions/js/extensions/prefs.js';

export default class NewBePreferences extends ExtensionPreferences {
    fillPreferencesWindow(window) {
        const settings = this.getSettings();

        window._settings = settings;

        const page = new Adw.PreferencesPage({
            title: 'NewBe',
            icon_name: 'preferences-desktop-appearance-symbolic',
        });

        const appearanceGroup = new Adw.PreferencesGroup({
            title: 'Appearance',
            description: 'Configure the NewBe GNOME Shell experience.',
        });

        const panelRow = new Adw.SwitchRow({
            title: 'Show NewBe panel label',
            subtitle: 'Display the NewBe identifier in the top panel.',
        });

        settings.bind(
            'show-panel-label',
            panelRow,
            'active',
            0
        );

        appearanceGroup.add(panelRow);

        const motionGroup = new Adw.PreferencesGroup({
            title: 'Motion',
            description: 'Choose how NewBe should feel when moving through the desktop.',
        });

        const motionModel = new Gtk.StringList();

        motionModel.append('Reduced');
        motionModel.append('Standard');
        motionModel.append('Fluid');

        const motionRow = new Adw.ComboRow({
            title: 'Motion profile',
            subtitle: 'Fluid will be the recommended NewBe experience.',
            model: motionModel,
        });

        const profiles = [
            'reduced',
            'standard',
            'fluid',
        ];

        const currentProfile = settings.get_string('motion-profile');
        const currentIndex = Math.max(profiles.indexOf(currentProfile), 0);

        motionRow.selected = currentIndex;

        motionRow.connect('notify::selected', row => {
            settings.set_string(
                'motion-profile',
                profiles[row.selected]
            );
        });

        motionGroup.add(motionRow);

        page.add(appearanceGroup);
        page.add(motionGroup);

        window.add(page);
    }
}
