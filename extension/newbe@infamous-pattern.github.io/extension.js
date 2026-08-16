import Clutter from 'gi://Clutter';
import St from 'gi://St';

import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import * as PopupMenu from 'resource:///org/gnome/shell/ui/popupMenu.js';

export default class NewBeExtension extends Extension {
    enable() {
        this._settings = this.getSettings();
        this._shellSettings = St.Settings.get();

        this._indicator = new PanelMenu.Button(
            0.0,
            this.metadata.name,
            false
        );

        this._indicator.add_style_class_name('newbe-panel-button');

        const box = new St.BoxLayout({
            style_class: 'newbe-panel-content',
            y_align: Clutter.ActorAlign.CENTER,
        });

        const mark = new St.Label({
            text: 'B',
            style_class: 'newbe-panel-mark',
            y_align: Clutter.ActorAlign.CENTER,
        });

        const label = new St.Label({
            text: 'NewBe',
            style_class: 'newbe-panel-label',
            y_align: Clutter.ActorAlign.CENTER,
        });

        box.add_child(mark);
        box.add_child(label);
        this._indicator.add_child(box);

        this._appearanceItem = new PopupMenu.PopupMenuItem('', {
            reactive: false,
            can_focus: false,
        });

        this._motionItem = new PopupMenu.PopupMenuItem('', {
            reactive: false,
            can_focus: false,
        });

        this._indicator.menu.addMenuItem(this._appearanceItem);
        this._indicator.menu.addMenuItem(this._motionItem);

        this._indicator.menu.addMenuItem(
            new PopupMenu.PopupSeparatorMenuItem()
        );

        this._indicator.menu.addAction(
            'NewBe Settings',
            () => this.openPreferences()
        );

        Main.panel.addToStatusArea(
            this.uuid,
            this._indicator,
            0,
            'left'
        );

        this._settingsChangedIds = [
            this._settings.connect(
                'changed::show-panel-label',
                () => this._syncIndicator()
            ),
            this._settings.connect(
                'changed::motion-profile',
                () => this._syncMotionProfile()
            ),
        ];

        this._colorSchemeChangedId =
            this._shellSettings.connect(
                'notify::color-scheme',
                () => this._syncAppearance()
            );

        this._syncIndicator();
        this._syncMotionProfile();
        this._syncAppearance();
    }

    disable() {
        if (this._settings) {
            for (const id of this._settingsChangedIds ?? [])
                this._settings.disconnect(id);
        }

        if (this._shellSettings && this._colorSchemeChangedId) {
            this._shellSettings.disconnect(
                this._colorSchemeChangedId
            );
        }

        this._settingsChangedIds = [];
        this._colorSchemeChangedId = null;

        this._indicator?.destroy();
        this._indicator = null;

        this._appearanceItem = null;
        this._motionItem = null;
        this._shellSettings = null;
        this._settings = null;
    }

    _syncIndicator() {
        if (!this._indicator || !this._settings)
            return;

        this._indicator.visible =
            this._settings.get_boolean('show-panel-label');
    }

    _syncMotionProfile() {
        if (!this._motionItem || !this._settings)
            return;

        const profile =
            this._settings.get_string('motion-profile');

        const displayNames = {
            reduced: 'Reduced',
            standard: 'Standard',
            fluid: 'Fluid',
        };

        this._motionItem.label.text =
            `Motion: ${displayNames[profile] ?? 'Fluid'}`;
    }

    _syncAppearance() {
        if (!this._indicator || !this._shellSettings)
            return;

        const scheme = this._shellSettings.color_scheme;

        /*
         * St.SystemColorScheme:
         * 0 = DEFAULT
         * 1 = PREFER_DARK
         * 2 = PREFER_LIGHT
         */
        const dark = scheme === 1;

        this._indicator.remove_style_class_name('newbe-light');
        this._indicator.remove_style_class_name('newbe-dark');

        this._indicator.add_style_class_name(
            dark ? 'newbe-dark' : 'newbe-light'
        );

        this._appearanceItem.label.text =
            `Appearance: ${dark ? 'Dark' : 'Light'}`;
    }
}
